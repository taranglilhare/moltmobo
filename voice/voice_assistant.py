"""
Voice Assistant Module
Handles Speech-to-Text (STT) and Text-to-Speech (TTS) for the agent.
Uses offline libraries for privacy and speed.
"""

import sys
import os
import threading
from utils.logger import logger

# Try importing voice libraries
try:
    import speech_recognition as sr
    import pyttsx3
    VOICE_AVAILABLE = True
except ImportError:
    VOICE_AVAILABLE = False
    logger.warning("Voice libraries not installed. Install with: pip install SpeechRecognition pyttsx3 pyaudio")

class VoiceAssistant:
    def __init__(self):
        self.enabled = VOICE_AVAILABLE
        if self.enabled:
            self.recognizer = sr.Recognizer()
            self.engine = pyttsx3.init()
            self._configure_voice()
        else:
            logger.warning("Voice Assistant disabled due to missing dependencies")

    def _configure_voice(self):
        """Configure TTS voice"""
        try:
            voices = self.engine.getProperty('voices')
            # Prefer a female voice if available (usually index 1 on Windows, varies on Linux)
            if len(voices) > 1:
                self.engine.setProperty('voice', voices[1].id)
            self.engine.setProperty('rate', 170) # Slightly faster
        except Exception as e:
            logger.error(f"Error configuring voice: {e}")

    def speak(self, text: str):
        """Speak text using TTS"""
        if not self.enabled:
            print(f"🤖 (Text-only): {text}")
            return
            
        logger.info(f"🗣️ Speaking: {text}")
        try:
            # Run in separate thread to not block
            threading.Thread(target=self._speak_thread, args=(text,)).start()
        except Exception as e:
             logger.error(f"TTS Error: {e}")

    def _speak_thread(self, text: str):
         self.engine.say(text)
         self.engine.runAndWait()

    def listen(self) -> str:
        """Listen for voice command"""
        if not self.enabled:
            logger.error("Voice not available")
            return ""

        with sr.Microphone() as source:
            logger.info("🎤 Listening...")
            self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
            try:
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=10)
                logger.info("Processing audio...")
                text = self.recognizer.recognize_google(audio)
                logger.info(f"👂 Heard: '{text}'")
                return text
            except sr.WaitTimeoutError:
                logger.info("Listening timed out.")
                return ""
            except sr.UnknownValueError:
                logger.info("Could not understand audio.")
                return ""
            except Exception as e:
                logger.error(f"Listening error: {e}")
                return ""

if __name__ == "__main__":
    if not VOICE_AVAILABLE:
        print("Install: pip install SpeechRecognition pyttsx3 pyaudio")
        sys.exit(1)
        
    va = VoiceAssistant()
    va.speak("Hello! I am Molt Mobo, your sovereign agent.")
    command = va.listen()
    if command:
        va.speak(f"You said: {command}")
