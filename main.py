import speech_recognition as sr
import webbrowser
import pyttsx3
import os
import time
import pyautogui
import pywhatkit
import keyboard
from openai import OpenAI
from dotenv import load_dotenv
import pygame
import numpy as np
import uuid

load_dotenv()

client = OpenAI(
    base_url="https://models.github.ai/inference",
    api_key=os.getenv("GITHUB_TOKEN"),
)
MODEL_NAME = "openai/gpt-4.1-mini"

# Initialize pygame for beep sounds
pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)

# Initialize TTS engine once (more efficient)
engine = pyttsx3.init()
voices = engine.getProperty("voices")
engine.setProperty("voice", voices[0].id)  # Change to voices[1].id for different voice
engine.setProperty("rate", 173)    # Try: 150 (slower), 173 (current), 200 (faster)
engine.setProperty("volume", 1.0)

# ==================== CONFIGURATION ====================
USE_WAKE_WORD = True  # Set to False to use push-to-talk (SPACE key)
WAKE_WORDS = ["jarvis", "hey jarvis", "ok jarvis"]

# ------------------ BEEP SOUND ------------------
def beep():
    """JARVIS-style double beep - cross-platform"""
    try:
        sample_rate = 22050
        
        # First beep - high
        t1 = np.linspace(0, 0.08, int(sample_rate * 0.08))
        beep1 = np.sin(2 * np.pi * 1200 * t1)
        
        # Silence
        silence = np.zeros(int(sample_rate * 0.03))
        
        # Second beep - lower
        t2 = np.linspace(0, 0.08, int(sample_rate * 0.08))
        beep2 = np.sin(2 * np.pi * 900 * t2)
        
        # Combine
        samples = np.concatenate([beep1, silence, beep2])
        samples = (samples * 20000).astype(np.int16)
        
        # Make stereo
        stereo = np.column_stack((samples, samples))
        sound = pygame.sndarray.make_sound(stereo)
        sound.play()
        pygame.time.wait(200)
    except:
        # Fallback to simple beep
        print('\a', end='', flush=True)

# ------------------ SPEAK ------------------
def speak(text):
    """Text to speech - reliable pyttsx3 version"""
    for sentence in text.split("."):
        if sentence.strip():
            engine.say(sentence.strip())
            engine.runAndWait()
            time.sleep(0.15)

# ------------------ AI RESPONSE (OpenAI) ------------------
def ai_response(query):
    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": "You are Jarvis, a helpful voice assistant. Keep responses concise for voice interaction."},
                {"role": "user", "content": query}
            ],
            max_tokens=150
        )

        reply = response.choices[0].message.content
        print("AI:", reply)
        speak(reply)

    except Exception as e:
        print("GitHub Models error:", e)
        speak("Sorry, I could not reach the AI service.")

# ------------------ LISTEN ------------------
def listen():
    """Listen for user command after wake word"""
    recognizer = sr.Recognizer()

    # Better noise handling
    recognizer.energy_threshold = 300
    recognizer.dynamic_energy_threshold = True
    recognizer.pause_threshold = 0.8

    try:
        with sr.Microphone() as source:
            print("Listening for command...")
            recognizer.adjust_for_ambient_noise(source, duration=0.5)
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=6)
    except Exception as e:
        print("Microphone error:", e)
        return ""

    try:
        command = recognizer.recognize_google(audio)
        print("You said:", command)
        return command.lower()
    except sr.UnknownValueError:
        print("Could not understand")
        return ""
    except sr.RequestError:
        speak("Network error")
        return ""

# ------------------ WAKE WORD DETECTION ------------------
def wait_for_wake_word():
    """
    Continuously listen for wake word (Jarvis/Hey Jarvis)
    Returns True when wake word is detected
    """
    recognizer = sr.Recognizer()
    recognizer.energy_threshold = 300
    recognizer.dynamic_energy_threshold = True
    recognizer.pause_threshold = 0.8
    
    print("🎤 Listening for wake word... (Say 'Jarvis' or 'Hey Jarvis')")
    
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        
        while True:
            try:
                # Listen for wake word (continuous listening)
                audio = recognizer.listen(source, timeout=None, phrase_time_limit=3)
                
                try:
                    text = recognizer.recognize_google(audio).lower()
                    print(f"Heard: '{text}'", end="")
                    
                    # Check for wake words
                    for wake_word in WAKE_WORDS:
                        if wake_word in text:
                            print(" ✓ Wake word detected!")
                            return True
                    
                    print(" (not wake word)")
                        
                except sr.UnknownValueError:
                    # Couldn't understand, keep listening
                    continue
                except sr.RequestError as e:
                    print(f"Network error: {e}")
                    time.sleep(1)
                    
            except KeyboardInterrupt:
                raise
            except Exception as e:
                print(f"Error: {e}")
                time.sleep(0.5)

# ------------------ PUSH TO TALK ------------------
def wait_for_push_to_talk():
    """Alternative: Press SPACE to activate"""
    print("Press SPACE and speak...")
    keyboard.wait("space")

# ------------------ SPOTIFY CONTROLS ------------------
def open_spotify():
    speak("Opening Spotify")
    spotify_path = os.getenv("SPOTIFY_PATH", "spotify")
    try:
        if os.name == 'nt':  # Windows
            os.startfile(spotify_path)
        else:  # Mac/Linux
            os.system(f'open -a "{spotify_path}"' if os.name == 'darwin' else 'spotify &')
    except:
        os.system("spotify")
    time.sleep(5)

def next_song():
    speak("Next song")
    pyautogui.press("nexttrack")

def previous_song():
    speak("Previous song")
    pyautogui.press("prevtrack")

# ------------------ COMMAND PROCESSOR ------------------
def process_command(command):
    if "open google" in command:
        speak("Opening Google")
        webbrowser.open("https://www.google.com")

    elif "open youtube" in command:
        speak("Opening YouTube")
        webbrowser.open("https://www.youtube.com")

    elif "open spotify" in command:
        open_spotify()

    elif "next song" in command:
        next_song()

    elif "previous song" in command:
        previous_song()

    elif "pause music" in command or "pause" in command:
        speak("Pausing")
        pyautogui.press("playpause")

    elif "play music" in command or "resume" in command:
        speak("Resuming")
        pyautogui.press("playpause")

    elif "play" in command:
        song = command.replace("play", "").strip()
        if song:
            play_song_youtube(song)
        else:
            speak("Please tell the song name")

    elif "stop listening" in command or "go to sleep" in command:
        speak("Going to sleep. Say Jarvis to wake me up.")
        return "sleep"

    elif "exit" in command or "shutdown" in command or "goodbye" in command:
        speak("Goodbye")
        cleanup_temp_files()
        exit()

    else:
        # Ask AI for anything else
        ai_response(command)

# ------------------ PLAY SONG BY VOICE ------------------
def play_song_youtube(song_name):
    speak(f"Playing {song_name} on YouTube")
    pywhatkit.playonyt(song_name)

def lower_volume(levels=8):
    for _ in range(levels):
        pyautogui.press("volumedown")

def restore_volume(levels=8):
    for _ in range(levels):
        pyautogui.press("volumeup")

def cleanup_temp_files():
    """Clean up any leftover temp speech files"""
    import glob
    for file in glob.glob("speech_*.mp3") + glob.glob("temp_speech*.mp3"):
        try:
            os.remove(file)
        except:
            pass

# ------------------ MAIN LOOP ------------------
if __name__ == "__main__":
    # Clean up any old temp files from previous runs
    cleanup_temp_files()
    
    if USE_WAKE_WORD:
        speak("Jarvis is online. Say Jarvis to activate me.")
        print("\n" + "="*60)
        print("🤖 JARVIS - WAKE WORD MODE")
        print("="*60)
        print("Say 'Jarvis' or 'Hey Jarvis' to activate")
        print("Then give your command")
        print("Say 'go to sleep' to pause wake word")
        print("Say 'exit' or 'shutdown' to quit")
        print("="*60 + "\n")
    else:
        speak("Jarvis is online. Press space to talk.")
        print("\n" + "="*60)
        print("🤖 JARVIS - PUSH-TO-TALK MODE")
        print("="*60)
        print("Press SPACE to activate")
        print("Say 'exit' to quit")
        print("="*60 + "\n")

    while True:
        try:
            # Wait for activation
            if USE_WAKE_WORD:
                wait_for_wake_word()
            else:
                wait_for_push_to_talk()
            
            # Play activation sound
            lower_volume()
            beep()
            
            # Listen for command
            query = listen()
            restore_volume()

            if not query or len(query) < 2:
                continue

            # Process command
            result = process_command(query)
            
            # Handle sleep mode
            if result == "sleep":
                # Keep looping but skip the beep
                continue
            
        except KeyboardInterrupt:
            print("\n\nShutting down...")
            speak("Shutting down")
            cleanup_temp_files()
            break
        except Exception as e:
            print(f"Error in main loop: {e}")
            time.sleep(1)