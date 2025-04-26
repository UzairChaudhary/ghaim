import joblib

# Try loading weather model
try:
    weather_model = joblib.load("weather_model.pkl")
    print(" Weather model loaded successfully.")
    print("Weather model type:", type(weather_model))
except Exception as e:
    print(" Failed to load weather model:", e)

# Try loading place model
try:
    place_model = joblib.load("place_model.pkl")
    print(" Place model loaded successfully.")
    print("Place model type:", type(place_model))
except Exception as e:
    print(" Failed to load place model:", e)
