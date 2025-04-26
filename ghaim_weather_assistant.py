import speech_recognition as sr
import pyttsx3
from datetime import datetime, timedelta
from ghaim_ml import predictor
import re
import time

class GhaimAssistant:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()

        self.engine = pyttsx3.init()
        self.configure_voice()

        self.available_emirates = list(predictor.emirate_encoder.classes_)

    def configure_voice(self):
        voices = self.engine.getProperty('voices')
        self.engine.setProperty('voice', voices[1].id)  # Microsoft Zira
        self.engine.setProperty('rate', 165)
        self.engine.setProperty('volume', 1.0)

    def speak(self, text):
        clean_text = re.sub(r'[^\w\s.,!?]', '', text)
        print(f"Ghaim: {clean_text}")
        self.engine.say(clean_text)
        self.engine.runAndWait()

    def listen(self, timeout=10, phrase_time_limit=8):
        with self.microphone as source:
            print("\nListening... (speak now)")
            try:
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                audio = self.recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
                text = self.recognizer.recognize_google(audio)
                print(f"You: {text}")
                return text.lower()
            except sr.WaitTimeoutError:
                self.speak("I didn't hear anything. Please respond faster next time.")
                return None
            except sr.UnknownValueError:
                self.speak("Sorry, I couldn't understand that. Please repeat.")
                return None
            except sr.RequestError as e:
                self.speak("Speech recognition service failed.")
                print(f"Error: {e}")
                return None

    def parse_query(self, text):
        if not text:
            return None, None

        emirate = next((e for e in self.available_emirates if e.lower() in text), None)

        today = datetime.today().date()
        if 'today' in text:
            date = today
        elif 'tomorrow' in text:
            date = today + timedelta(days=1)
        else:
            date_match = re.search(r'(\d{4})[-/](\d{1,2})[-/](\d{1,2})', text)
            if date_match:
                y, m, d = map(int, date_match.groups())
                date = datetime(y, m, d).date()
            else:
                date = None

        return emirate, date

    def provide_recommendations(self, emirate, weather):
        recs = predictor.get_recommendations(emirate, weather)
        self.speak(f"Here are top suggestions in {emirate.title()} for {weather} weather.")
        for category, places in recs.items():
            if places:
                self.speak(f"{category} options include:")
                for place in places[:3]:
                    self.speak(place)

    def run(self):
        self.speak("Hello! I'm Ghaim, your UAE weather assistant. How can I help you today?")

        while True:
            text = self.listen()
            if not text:
                continue

            if any(word in text for word in ['exit', 'quit', 'goodbye']):
                self.speak("Goodbye! Stay safe and enjoy the UAE!")
                break

            emirate, date = self.parse_query(text)
            if not emirate:
                self.speak("Please mention a valid UAE emirate.")
                continue
            if not date:
                self.speak("Please say a date like 'today', 'tomorrow', or a full date.")
                continue

            try:
                weather, _ = predictor.get_weather_and_place(emirate, date)
                self.speak(f"The weather in {emirate.title()} on {date.strftime('%A, %B %d')} is expected to be {weather}.")

                self.speak("Would you like recommendations for places to visit?")
                confirm = self.listen()
                print("DEBUG — Heard after prompt:", confirm)
                if confirm:
                    if any(key in confirm for key in ['yes', 'sure', 'okay', 'places', 'visit', 'recommend', 'suggest']):
                        print("DEBUG — Match accepted, providing recommendations...")
                        self.provide_recommendations(emirate, weather)
                    else:
                        print("DEBUG — Heard something unrelated. Skipping recommendations.")
                else:
                    self.speak("Didn't catch that, skipping recommendations.")

            except Exception as e:
                print(f"Error: {e}")
                self.speak("Sorry, something went wrong while processing that.")

if __name__ == "__main__":
    assistant = GhaimAssistant()
    assistant.run()
