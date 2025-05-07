import streamlit as st
import pandas as pd

#Drill-down operation in this code aggregates and displays detailed city-level traffic and accident data from higher-level location-based data.

# Drill-down operation in OLAP
def drilldown(traffic_data, weather_data, accident_history):
    st.subheader("🔽 Drill-Down Operation (Higher to Lower Level Details)")

    # Standardize column names to lowercase and strip spaces
    traffic_data.columns = traffic_data.columns.str.strip().str.lower()
    accident_history.columns = accident_history.columns.str.strip().str.lower()
    weather_data.columns = weather_data.columns.str.strip().str.lower()

    # Validate required columns
    required_traffic_cols = {'location', 'city', 'traffic volume'}
    required_accident_cols = {'location', 'accident count'}

    if not required_traffic_cols.issubset(set(traffic_data.columns)):
        st.error("Traffic data is missing required columns.")
        st.write("Expected columns:", required_traffic_cols)
        st.write("Found columns:", traffic_data.columns.tolist())
        return

    if not required_accident_cols.issubset(set(accident_history.columns)):
        st.error("Accident data is missing required columns.")
        st.write("Expected columns:", required_accident_cols)
        st.write("Found columns:", accident_history.columns.tolist())
        return

    # Merge traffic and accident data on 'location'
    merged_df = pd.merge(traffic_data, accident_history, on='location', how='inner')

    # Aggregate drill-down data at city level
    city_level_data = merged_df.groupby('city').agg(
        total_traffic_volume=pd.NamedAgg(column='traffic volume', aggfunc='sum'),
        total_accident_count=pd.NamedAgg(column='accident count', aggfunc='sum')
    ).reset_index().sort_values(by='total_traffic_volume', ascending=False)

    # Display result
    st.dataframe(city_level_data, use_container_width=True)
    st.success("Drill-down to city-level traffic and accident data completed.")
