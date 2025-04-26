from datetime import datetime, timedelta
from ghaim_ml import predictor
import matplotlib.pyplot as plt
import pandas as pd

def display_weather_recommendations(emirate, date, weather, places):
    print("\n" + "="*60)
    print(f"\U0001F30D WEATHER REPORT FOR {emirate.upper()} - {date.strftime('%A, %B %d, %Y')}")
    print("="*60)

    weather_icons = {
        'sunny': '☀️', 'rainy': '🌧️', 'cloudy': '☁️',
        'windy': '🌬️', 'stormy': '⛈️', 'foggy': '🌫️'
    }
    icon = weather_icons.get(weather.lower(), '🌡️')
    print(f"\n{icon} Expected Weather: {weather.upper()} {icon}\n")

    want_recs = input("\nWould you like recommendations for places to visit? (yes/no): ").strip().lower()
    if want_recs in ['yes', 'y']:
        print("\n\U0001F31F RECOMMENDED PLACES:")
        for category, suggestions in places.items():
            if suggestions:
                print(f"\n{category.upper()}:")
                for i, place in enumerate(suggestions, 1):
                    print(f"  {i}. {place}")


def manual_mode():
    print("\n" + "="*60)
    print("🇦🇪 UAE WEATHER PREDICTION AND RECOMMENDATION SYSTEM")
    print("="*60)
    print("\nThis system predicts weather and suggests places to visit in all 7 UAE emirates.\n")

    available_emirates = list(predictor.emirate_encoder.classes_)

    while True:
        try:
            print("\nAvailable Emirates:")
            for i, emirate in enumerate(available_emirates, 1):
                print(f"{i}. {emirate.title()}")

            emirate_choice = input("\nEnter the number or name of the emirate (or 'exit' to quit): ").strip()
            if emirate_choice.lower() in ['exit', 'quit']:
                print("\nThank you for using the UAE Weather Prediction System!")
                break

            if emirate_choice.isdigit():
                idx = int(emirate_choice) - 1
                if 0 <= idx < len(available_emirates):
                    emirate = available_emirates[idx]
                else:
                    print("⚠️ Invalid number. Please try again.")
                    continue
            else:
                if emirate_choice in available_emirates:
                    emirate = emirate_choice
                else:
                    print("⚠️ Invalid emirate name. Please try again.")
                    continue

            today = datetime.today().date()
            print("\nDate Options:")
            print(f"1. Today ({today})")
            print(f"2. Tomorrow ({today + timedelta(days=1)})")
            print("3. Select a specific date")

            date_choice = input("\nEnter your choice (1-3): ").strip()
            if date_choice == '1':
                date = today
            elif date_choice == '2':
                date = today + timedelta(days=1)
            elif date_choice == '3':
                date_str = input("Enter date (YYYY-MM-DD): ").strip()
                try:
                    date = datetime.strptime(date_str, "%Y-%m-%d").date()
                    if date < today:
                        print("⚠️ Note: You've selected a date in the past.")
                except ValueError:
                    print("⚠️ Invalid date format. Please use YYYY-MM-DD.")
                    continue
            else:
                print("⚠️ Invalid choice. Please try again.")
                continue

            print("\n🔮 Predicting weather...")
            weather, places = predictor.get_weather_and_place(emirate, date)

            display_weather_recommendations(emirate, date, weather, places)

            again = input("\nWould you like to check another emirate/date? (yes/no): ").strip().lower()
            if again not in ['yes', 'y']:
                print("\nThank you for using the UAE Weather Prediction System!")
                break

        except Exception as e:
            print(f"\n⚠️ An error occurred: {str(e)}")
            print("Please try again.\n")

if __name__ == "__main__":
    manual_mode()
