import pandas as pd

def load_data():
    traffic_df = pd.read_csv('data/traffic_data.csv')
    weather_df = pd.read_csv('data/weather_data.csv')
    accident_df = pd.read_csv('data/accident_history.csv')
    return traffic_df, weather_df, accident_df
