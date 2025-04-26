import speech_recognition as sr

recognizer = sr.Recognizer()
mic = sr.Microphone()

print("🎙️ Speak something after the beep...")

with mic as source:
    recognizer.adjust_for_ambient_noise(source)
    audio = recognizer.listen(source, timeout=10, phrase_time_limit=5)

try:
    result = recognizer.recognize_google(audio)
    print(f"✅ Recognized: {result}")
except sr.UnknownValueError:
    print("❌ Could not understand audio.")
except sr.RequestError as e:
    print(f"❌ Request failed: {e}")
except sr.WaitTimeoutError:
    print("⌛ Timeout — no voice detected.")
