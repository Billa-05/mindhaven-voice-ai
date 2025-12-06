# MindHaven Voice AI – Multi-Voice Emotional Assistant
# Author: Mrudula Billa

import speech_recognition as sr
from transformers import pipeline
import pyttsx3

class EmotionalVoiceBot:
    def __init__(self, voice_type="female"):
        # Voice settings
        self.engine = pyttsx3.init()
        voices = self.engine.getProperty("voices")

        # Assign voice based on user choice
        if voice_type == "male":
            self.engine.setProperty("voice", voices[0].id)   # Male voice
        elif voice_type == "female":
            self.engine.setProperty("voice", voices[1].id)   # Female voice
        elif voice_type == "kid":
            self.engine.setProperty("voice", voices[1].id)   # Female voice + high pitch
            self.engine.setProperty("pitch", 150)
        else:
            self.engine.setProperty("voice", voices[1].id)

        self.engine.setProperty("rate", 170)  # normal speed
        self.engine.setProperty("volume", 1.0)

        # AI models
        self.recognizer = sr.Recognizer()
        self.sentiment_model = pipeline("sentiment-analysis")

    # 🎤 Convert voice → text
    def listen(self):
        with sr.Microphone() as source:
            print("Listening...")
            audio = self.recognizer.listen(source)

        try:
            text = self.recognizer.recognize_google(audio)
            print("User said:", text)
            return text
        except:
            return "Sorry, I didn't hear anything clearly."

    # 🧠 Detect mood
    def analyze_mood(self, text):
        result = self.sentiment_model(text)[0]
        return result["label"]

    # 💬 Supportive AI reply
    def reply(self, text):
        mood = self.analyze_mood(text)

        if mood == "NEGATIVE":
            return "I am here with you. Take a slow breath. You are safe."
        elif mood == "POSITIVE":
            return "That is wonderful! I am happy to hear something positive from you."
        else:
            return "Thank you for sharing. I am here to support you."

    # 🔊 Speak the response
    def speak(self, text):
        self.engine.say(text)
        self.engine.runAndWait()

    # 🚀 Start full session
    def start_voice_session(self):
        text = self.listen()
        response = self.reply(text)
        print("AI:", response)
        self.speak(response)
