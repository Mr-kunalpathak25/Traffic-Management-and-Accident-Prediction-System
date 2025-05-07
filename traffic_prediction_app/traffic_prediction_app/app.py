import streamlit as st
import pandas as pd

from models.multidimensional_model import load_data
from olap_operations.rollup import rollup
from olap_operations.drilldown import drilldown
from olap_operations.slice import slice_operation
from olap_operations.dice import dice_operation
from utils.concept_hierarchy import show_hierarchies
from prediction.predict_accidents import predict_accident_zones

# Load Data
traffic_data, weather_data, accident_history = load_data()

st.title("🚦 Traffic Management & Accident Prediction System")

# Sidebar for OLAP Operations
operation = st.sidebar.selectbox(
    "Select OLAP Operation", 
    ["Roll-up", "Drill-down", "Slice", "Dice", "Concept Hierarchies", "Predict Accident Zones"]
)

if operation == "Roll-up":
    rollup(traffic_data, weather_data, accident_history)

elif operation == "Drill-down":
    drilldown(traffic_data, weather_data, accident_history)

elif operation == "Slice":
    slice_operation(traffic_data, weather_data, accident_history)

elif operation == "Dice":
    dice_operation(traffic_data, weather_data, accident_history)

elif operation == "Concept Hierarchies":
    show_hierarchies()

elif operation == "Predict Accident Zones":
    predict_accident_zones(traffic_data, weather_data, accident_history)
