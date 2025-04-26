import pandas as pd
import joblib
from datetime import datetime
import os

class WeatherPredictor:
    def __init__(self):
        print("✅ WeatherPredictor initialized with generalizable ML model.")
        self.weather_model = joblib.load("weather_model.pkl")
        self.place_model = joblib.load("place_model.pkl")
        self.emirate_encoder = joblib.load("emirate_encoder.pkl")
        self.weather_encoder = joblib.load("weather_encoder.pkl")

        self.places_data = self._load_and_clean_data("UAE_Places_All_Emirates.csv")
        self._validate_data()

    def _load_and_clean_data(self, filename):
        if not os.path.exists(filename):
            raise FileNotFoundError(f"Missing file: {filename}")
        df = pd.read_csv(filename, encoding="cp1252")
        if 'Emirate' in df.columns:
            df['Emirate'] = df['Emirate'].str.strip()
        if 'Weather Category' in df.columns:
            df['Weather Category'] = df['Weather Category'].str.strip().str.lower()
        if 'Category' in df.columns:
            df['Category'] = df['Category'].str.strip()
        return df

    def _validate_data(self):
        if not {'Emirate', 'Weather Category', 'Category', 'Suggested Place'}.issubset(self.places_data.columns):
            raise ValueError("Places data missing required columns")

    def predict_weather(self, emirate, date):
        if isinstance(date, str):
            date = datetime.strptime(date, "%Y-%m-%d").date()

        emirate = emirate.strip()
        if emirate not in self.emirate_encoder.classes_:
            raise ValueError(f"Unknown emirate: {emirate}")

        emirate_encoded = self.emirate_encoder.transform([emirate])[0]

        features = pd.DataFrame([{
            "Emirate_Encoded": emirate_encoded,
            "Year": date.year,
            "Month": date.month,
            "Day": date.day
        }])

        print("🧪 Predicting with features:")
        print(features)

        weather_encoded = self.weather_model.predict(features)[0]
        print(f"🔢 Encoded prediction: {weather_encoded}")

        weather = self.weather_encoder.inverse_transform([weather_encoded])[0]
        print(f"🌤️ Predicted weather label: {weather}")
        return weather

    def get_recommendations(self, emirate, weather):
        emirate = emirate.strip()
        weather = weather.strip().lower()

        print(f"\n📂 Searching for places in {emirate} with weather category like: {weather}")

        df = self.places_data.copy()
        df['Emirate'] = df['Emirate'].str.strip()
        df['Weather Category'] = df['Weather Category'].str.strip().str.lower()
        df['Category'] = df['Category'].str.strip()

        # Final fuzzy logic: match if weather is in label OR label is in weather
        filtered = df[
            (df['Emirate'] == emirate) &
            (df['Weather Category'].apply(lambda x: (x in weather) or (weather in x)))
        ]

        print(f"🗂️ Matched {len(filtered)} rows for {emirate} - {weather}")

        recs = {}
        for cat in ['Indoor', 'Outdoor', 'Restaurants', 'Playing World']:
            matches = filtered[filtered['Category'] == cat]
            recs[cat] = matches['Suggested Place'].dropna().unique().tolist()[:5]
            print(f"📊 {cat}: {len(matches)} matches")

        return recs

    def get_weather_and_place(self, emirate, date):
        weather = self.predict_weather(emirate, date)
        recommendations = self.get_recommendations(emirate, weather)
        return weather, recommendations

predictor = WeatherPredictor()

def get_weather_and_place(emirate, date):
    return predictor.get_weather_and_place(emirate, date)
