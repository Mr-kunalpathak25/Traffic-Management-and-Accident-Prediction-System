import streamlit as st
import pandas as pd

# Map textual severity to numeric values
severity_map = {'Low': 1, 'Medium': 2, 'High': 3}

def load_data():
    try:
        traffic_df = pd.read_csv("traffic_data.csv")
        weather_df = pd.read_csv("weather_data.csv")
        accident_df = pd.read_csv("accident_history.csv")

        # Map 'Severity' to numeric, and handle any non-mappable values
        accident_df['Severity'] = accident_df['Severity'].map(severity_map)
        accident_df.dropna(subset=['Severity'], inplace=True)  # Drop rows where 'Severity' is NaN after mapping
        return traffic_df, weather_df, accident_df
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None, None, None

def predict_accident_zones(traffic_df, weather_df, accident_df):
    st.subheader("🧠 Predict Accident Prone Zones")

    if traffic_df is None or weather_df is None or accident_df is None:
        st.warning("Data not loaded properly.")
        return

    # Merge datasets on 'Location'
    merged = pd.merge(traffic_df, accident_df, on='Location', how='inner')
    merged = pd.merge(merged, weather_df, on='Location', how='inner')

    # Drop rows with missing values in any relevant column
    merged.dropna(subset=['Traffic Volume', 'Accident Count', 'Severity'], inplace=True)

    # Ensure the columns used for calculations are numeric
    merged['Traffic Volume'] = pd.to_numeric(merged['Traffic Volume'], errors='coerce')
    merged['Accident Count'] = pd.to_numeric(merged['Accident Count'], errors='coerce')

    # Check the type of 'Severity' column before performing operations
    print(merged['Severity'].dtype)
    print(merged['Severity'].head())

    # Convert 'Severity' to numeric, handling errors by coercing them to NaN
    merged['Severity'] = pd.to_numeric(merged['Severity'], errors='coerce')

    # Fill NaN values in 'Severity' with 0
    merged['Severity'] = merged['Severity'].fillna(0)
    #The weights reflect the relative importance of each factor in risk assessment, with accident count prioritized over traffic volume and severity.
    # Calculate Risk Score
    merged['Risk_Score'] = (merged['Traffic Volume'] * 0.4) + \
                           (merged['Accident Count'] * 0.5) + \
                           (merged['Severity'] * 0.1)

    # Assign Risk Category
    def label_risk(score):
        if score >= 1500:
            return "⚠️ High Risk"
        elif score >= 1000:
            return "⚠ Moderate Risk"
        else:
            return "✅ Low Risk"

    merged['Risk Level'] = merged['Risk_Score'].apply(label_risk)

    # Display top 10 risky zones
    top_risky_zones = merged.sort_values('Risk_Score', ascending=False).head(10)
    st.dataframe(top_risky_zones[['Location', 'City', 'State', 'Risk_Score', 'Risk Level']])
    st.success("These are the top 10 zones with the highest accident risk based on traffic, accidents, and severity.")

def main():
    st.title("🚦 Traffic Accident Risk Predictor")
    st.markdown("This tool uses traffic volume, past accident counts, and severity data to identify accident-prone zones.")

    traffic_df, weather_df, accident_df = load_data()
    if all([traffic_df is not None, weather_df is not None, accident_df is not None]):
        predict_accident_zones(traffic_df, weather_df, accident_df)

    # Add this line for clarification/debugging purposes
    st.write("This is the main function")

if __name__ == "__main__":
    main()
