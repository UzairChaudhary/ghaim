import pandas as pd
import joblib
from datetime import datetime
import os

class WeatherPredictor:
    def __init__(self):
        print("✅ WeatherPredictor initialized.")
        self.weather_model = joblib.load("weather_model.pkl")
        self.place_model = joblib.load("place_model.pkl")
        self.emirate_encoder = joblib.load("emirate_encoder.pkl")
        self.weather_encoder = joblib.load("weather_encoder.pkl")

        self.temperature_data = self._load_and_clean_data("UAE_Temperature_file.csv")
        self.places_data = self._load_and_clean_data("UAE_Places_file2 (1).csv")
        self._validate_data()

    def _load_and_clean_data(self, filename):
        if not os.path.exists(filename):
            raise FileNotFoundError(f"Missing file: {filename}")
        df = pd.read_csv(filename, encoding="cp1252")
        if 'Emirate' in df.columns:
            df['Emirate'] = df['Emirate'].str.strip()
        if 'Weather Category' in df.columns:
            df['Weather Category'] = df['Weather Category'].str.strip()
        return df

    def _validate_data(self):
        if not {'Emirate', 'Weather Category', 'Category', 'Suggested Place'}.issubset(self.places_data.columns):
            raise ValueError("Places data missing required columns")
        if not {'Emirate', 'Year', 'Month', 'Day', 'Temp_Max[?øC]', 'Temp_Mean[?øC]', 'Temp_Min[?øC]'}.issubset(self.temperature_data.columns):
            raise ValueError("Temperature data missing required columns")

    def predict_weather(self, emirate, date):
        if isinstance(date, str):
            date = datetime.strptime(date, "%Y-%m-%d").date()

        emirate = emirate.strip()
        if emirate not in self.emirate_encoder.classes_:
            raise ValueError(f"Unknown emirate: {emirate}")

        temp_row = self.temperature_data[
            (self.temperature_data['Emirate'] == emirate) &
            (self.temperature_data['Year'] == date.year) &
            (self.temperature_data['Month'] == date.month) &
            (self.temperature_data['Day'] == date.day)
        ]

        if temp_row.empty:
            raise ValueError("No temperature data available for the selected date and emirate")

        temp_max = temp_row.iloc[0]['Temp_Max[?øC]']
        temp_mean = temp_row.iloc[0]['Temp_Mean[?øC]']
        temp_min = temp_row.iloc[0]['Temp_Min[?øC]']

        emirate_encoded = self.emirate_encoder.transform([emirate])[0]

        features = pd.DataFrame([{
            "Emirate": emirate_encoded,
            "Year": date.year,
            "Month": date.month,
            "Day": date.day,
            "Temp_Max[?øC]": temp_max,
            "Temp_Mean[?øC]": temp_mean,
            "Temp_Min[?øC]": temp_min
        }])

        print("🧪 Prediction features:")
        print(features)

        weather_encoded = self.weather_model.predict(features)[0]
        print(f"🔢 Encoded prediction: {weather_encoded}")

        weather = self.weather_encoder.inverse_transform([weather_encoded])[0]
        print(f"🌤️ Predicted weather label: {weather}")
        return weather

    def get_recommendations(self, emirate, weather):
        emirate = emirate.strip()
        weather = weather.strip()
        filtered = self.places_data[
            (self.places_data['Emirate'] == emirate) &
            (self.places_data['Weather Category'] == weather)
        ]
        recs = {}
        for cat in ['Indoor', 'Outdoor', 'Restaurants', 'Playing World']:
            matches = filtered[filtered['Category'] == cat]
            recs[cat] = matches['Suggested Place'].dropna().unique().tolist()[:5]
        return recs

    def get_weather_and_place(self, emirate, date):
        weather = self.predict_weather(emirate, date)
        recommendations = self.get_recommendations(emirate, weather)
        return weather, recommendations

predictor = WeatherPredictor()

def get_weather_and_place(emirate, date):
    return predictor.get_weather_and_place(emirate, date)
