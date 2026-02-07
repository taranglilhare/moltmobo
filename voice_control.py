"""
Voice Control Module - Free Speech Recognition
Uses OpenAI Whisper for speech-to-text (100% free and offline)
"""

import os
from pathlib import Path
from typing import Optional
import subprocess

try:
    import whisper
    WHISPER_AVAILABLE = True
except ImportError:
    WHISPER_AVAILABLE = False

from utils.logger import logger


class VoiceControl:
    """Voice control using Whisper speech recognition"""
    
    def __init__(self, model_size: str = "tiny"):
        """
        Initialize voice control
        
        Args:
            model_size: Whisper model size (tiny, base, small, medium, large)
                       tiny: 39M params, fastest
                       base: 74M params
                       small: 244M params
                       medium: 769M params
        """
        self.model_size = model_size
        self.model = None
        self.enabled = False
        
        if not WHISPER_AVAILABLE:
            logger.warning("⚠️  Whisper not installed. Voice control disabled.")
            logger.info("Install with: pip install openai-whisper")
            return
        
        self._load_model()
    
    def _load_model(self):
        """Load Whisper model"""
        try:
            logger.info(f"Loading Whisper model: {self.model_size}...")
            self.model = whisper.load_model(self.model_size)
            self.enabled = True
            logger.info(f"✓ Whisper {self.model_size} loaded successfully")
        except Exception as e:
            logger.error(f"Failed to load Whisper: {e}")
    
    def record_audio(self, duration: int = 5, output_file: str = "/sdcard/voice_input.wav") -> bool:
        """
        Record audio using Termux API
        
        Args:
            duration: Recording duration in seconds
            output_file: Output file path
        
        Returns:
            True if successful
        """
        try:
            # Use termux-microphone-record
            logger.info(f"Recording audio for {duration} seconds...")
            
            # Start recording
            subprocess.run([
                "termux-microphone-record",
                "-f", output_file,
                "-l", str(duration)
            ], check=True)
            
            logger.info(f"✓ Audio recorded: {output_file}")
            return True
        
        except Exception as e:
            logger.error(f"Audio recording failed: {e}")
            return False
    
    def transcribe_audio(self, audio_file: str, language: str = None) -> Optional[str]:
        """
        Transcribe audio to text
        
        Args:
            audio_file: Path to audio file
            language: Optional language code (en, hi, es, etc.)
        
        Returns:
            Transcribed text or None
        """
        if not self.enabled:
            return None
        
        try:
            logger.info(f"Transcribing audio: {audio_file}...")
            
            # Transcribe
            result = self.model.transcribe(
                audio_file,
                language=language,
                fp16=False  # Use FP32 for CPU
            )
            
            text = result["text"].strip()
            logger.info(f"✓ Transcription: {text}")
            
            return text
        
        except Exception as e:
            logger.error(f"Transcription failed: {e}")
            return None
    
    def listen_for_command(self, duration: int = 5, language: str = None) -> Optional[str]:
        """
        Listen for voice command and return text
        
        Args:
            duration: Recording duration
            language: Optional language
        
        Returns:
            Command text or None
        """
        # Record audio
        audio_file = "/sdcard/moltmobo_voice.wav"
        
        if not self.record_audio(duration, audio_file):
            return None
        
        # Transcribe
        command = self.transcribe_audio(audio_file, language)
        
        # Cleanup
        try:
            os.remove(audio_file)
        except:
            pass
        
        return command
    
    def detect_language(self, audio_file: str) -> str:
        """
        Detect language from audio
        
        Args:
            audio_file: Path to audio file
        
        Returns:
            Language code
        """
        if not self.enabled:
            return "en"
        
        try:
            # Load audio and detect language
            audio = whisper.load_audio(audio_file)
            audio = whisper.pad_or_trim(audio)
            
            # Make log-Mel spectrogram
            mel = whisper.log_mel_spectrogram(audio).to(self.model.device)
            
            # Detect language
            _, probs = self.model.detect_language(mel)
            detected_lang = max(probs, key=probs.get)
            
            logger.info(f"Detected language: {detected_lang}")
            return detected_lang
        
        except Exception as e:
            logger.error(f"Language detection failed: {e}")
            return "en"
    
    def continuous_listen(self, callback, duration: int = 5, language: str = None):
        """
        Continuous listening mode
        
        Args:
            callback: Function to call with transcribed text
            duration: Duration per recording
            language: Optional language
        """
        logger.info("🎤 Continuous listening mode activated")
        logger.info("Say 'stop listening' to exit")
        
        while True:
            try:
                # Listen for command
                command = self.listen_for_command(duration, language)
                
                if not command:
                    continue
                
                # Check for stop command
                if "stop listening" in command.lower():
                    logger.info("Stopping continuous listening")
                    break
                
                # Execute callback
                callback(command)
            
            except KeyboardInterrupt:
                logger.info("Interrupted by user")
                break
            except Exception as e:
                logger.error(f"Continuous listening error: {e}")


class TextToSpeech:
    """Free text-to-speech using Piper"""
    
    def __init__(self):
        """Initialize TTS"""
        self.enabled = self._check_piper()
    
    def _check_piper(self) -> bool:
        """Check if Piper TTS is installed"""
        try:
            subprocess.run(["piper", "--version"], capture_output=True, check=True)
            logger.info("✓ Piper TTS available")
            return True
        except:
            logger.warning("⚠️  Piper TTS not installed")
            logger.info("Install: pkg install piper-tts")
            return False
    
    def speak(self, text: str, output_file: str = "/sdcard/tts_output.wav") -> bool:
        """
        Convert text to speech
        
        Args:
            text: Text to speak
            output_file: Output audio file
        
        Returns:
            True if successful
        """
        if not self.enabled:
            return False
        
        try:
            # Use Piper TTS
            process = subprocess.Popen(
                ["piper", "--output_file", output_file],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            
            process.communicate(input=text.encode())
            
            # Play audio using termux-media-player
            subprocess.run(["termux-media-player", "play", output_file])
            
            logger.info(f"✓ Spoke: {text}")
            return True
        
        except Exception as e:
            logger.error(f"TTS failed: {e}")
            return False
    
    def speak_async(self, text: str):
        """Speak without blocking"""
        import threading
        thread = threading.Thread(target=self.speak, args=(text,))
        thread.start()
