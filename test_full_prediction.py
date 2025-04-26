import joblib
import pandas as pd
from datetime import datetime

# Load models and encoders
weather_model = joblib.load("weather_model.pkl")
emirate_encoder = joblib.load("emirate_encoder.pkl")
weather_encoder = joblib.load("weather_encoder.pkl")

# Load temperature dataset
temperature_data = pd.read_csv("UAE_Temperature_file.csv", encoding='cp1252')
temperature_data['Emirate'] = temperature_data['Emirate'].str.strip()

# Input
emirate = "Dubai"
date = datetime(2025, 4, 23).date()

# Get temperature row
row = temperature_data[
    (temperature_data['Emirate'] == emirate) &
    (temperature_data['Year'] == date.year) &
    (temperature_data['Month'] == date.month) &
    (temperature_data['Day'] == date.day)
]

if row.empty:
    print("⚠️ No temperature data found for that date and emirate.")
else:
    temp_max = row.iloc[0]['Temp_Max[?øC]']
    temp_mean = row.iloc[0]['Temp_Mean[?øC]']
    temp_min = row.iloc[0]['Temp_Min[?øC]']

    emirate_encoded = emirate_encoder.transform([emirate])[0]

    features = pd.DataFrame([{
        "Emirate": emirate_encoded,
        "Year": date.year,
        "Month": date.month,
        "Day": date.day,
        "Temp_Max[?øC]": temp_max,
        "Temp_Mean[?øC]": temp_mean,
        "Temp_Min[?øC]": temp_min
    }])

    print("\n🧪 Input features to model:")
    print(features)

    # Predict
    predicted_encoded = weather_model.predict(features)[0]
    predicted_weather = weather_encoder.inverse_transform([predicted_encoded])[0]

    print(f"\n🌤️ Predicted weather for {emirate} on {date}: {predicted_weather}")
