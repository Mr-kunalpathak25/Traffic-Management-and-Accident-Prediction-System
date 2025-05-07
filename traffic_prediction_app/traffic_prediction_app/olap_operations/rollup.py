import streamlit as st
import pandas as pd

#Roll-up operation in this code aggregates traffic volume from lower levels (City) to higher levels (State) for summarized analysis

def rollup(traffic_df, weather_df, accident_df):
    st.subheader("🔼 Roll-up Operation (Lower to Higher Level Aggregation)")

    # Check if required columns exist
    required_columns = ['City', 'State', 'Traffic Volume']
    if not all(col in traffic_df.columns for col in required_columns):
        st.error("Missing required columns in traffic data.")
        return

    # Ensure 'Traffic Volume' is numeric
    traffic_df['Traffic Volume'] = pd.to_numeric(traffic_df['Traffic Volume'], errors='coerce')
    
    # Remove rows with missing values
    traffic_df.dropna(subset=['City', 'State', 'Traffic Volume'], inplace=True)

    # Roll-up at City level
    city_rollup = traffic_df.groupby('City', as_index=False)['Traffic Volume'].sum().sort_values(by='Traffic Volume', ascending=False)
    st.markdown("### 🚗 Traffic Volume by City")
    st.dataframe(city_rollup)

    # Roll-up at State level
    state_rollup = traffic_df.groupby('State', as_index=False)['Traffic Volume'].sum().sort_values(by='Traffic Volume', ascending=False)
    st.markdown("### 🛣️ Traffic Volume by State")
    st.dataframe(state_rollup)
