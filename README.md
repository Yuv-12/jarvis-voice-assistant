# 🤖 JARVIS - AI Voice Assistant

A Python-based AI voice assistant inspired by Iron Man's JARVIS. Features wake-word activation, AI-powered responses via GitHub Models, and comprehensive media control.

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![Status](https://img.shields.io/badge/status-active-success.svg)

## ✨ Features

- 🎙 **Wake-word detection** - Activate with "Jarvis" or "Hey Jarvis"
- 🖐 **Push-to-talk mode** - Alternative SPACE key activation
- 🧠 **AI-powered responses** - Using GitHub Models (free tier)
- 🔊 **Smart volume ducking** - Lowers volume during listening, restores after
- 🎵 **Media control** - Spotify & YouTube integration
  - Play/Pause music
  - Next/Previous track
  - Play songs on YouTube by voice
- 🗣 **Text-to-Speech** - Offline TTS using pyttsx3
- 🔔 **Custom JARVIS beep** - Authentic activation sound
- 🌐 **Web automation** - Open Google, YouTube, and more
- 🧼 **Resource-safe** - No mic locking or temp file leaks

## 🏗 System Architecture

```
            User Speech
                ↓
  SpeechRecognition (Google STT)
                ↓
          Command Router
 ┌───────────────┬─────────────────┐
 │ System Tasks  │ AI Queries      │
 │ (Media/Web)   │ (GitHub Models) │
 └───────────────┴─────────────────┘
                ↓
      Text-to-Speech (pyttsx3)
```

## 🛠 Technologies Used

| Technology | Purpose |
|------------|---------|
| `speech_recognition` | Speech-to-text conversion |
| `pyttsx3` | Offline text-to-speech |
| `pyautogui` | Media & system control |
| `pywhatkit` | YouTube playback |
| `keyboard` | Push-to-talk input |
| `pygame` + `numpy` | Custom beep sound generation |
| `openai` | GitHub Models API client |
| `python-dotenv` | Environment variable management |

## 📋 Prerequisites

- Python 3.8 or higher
- Microphone access
- Internet connection (for speech recognition and AI)
- (Optional) Spotify installed for media control

## ⚙️ Installation

### 1️⃣ Clone the repository
```bash
git clone https://github.com/YOUR-USERNAME/jarvis-voice-assistant.git
cd jarvis-voice-assistant
```

### 2️⃣ Create virtual environment (recommended)
```bash
python -m venv .venv
```

**Activate the environment:**

**Windows:**
```bash
.venv\Scripts\activate
```

**Linux/macOS:**
```bash
source .venv/bin/activate
```

### 3️⃣ Install dependencies
```bash
pip install -r requirements.txt
```

### 4️⃣ Set up environment variables

Create a `.env` file in the project root:

```env
GITHUB_TOKEN=your_github_models_api_key
SPOTIFY_PATH=path_to_spotify_executable
```

**Example (Windows):**
```env
GITHUB_TOKEN=ghp_xxxxxxxxxxxxxxxxxxxx
SPOTIFY_PATH=C:\Users\YourName\AppData\Roaming\Spotify\Spotify.exe
```

**Example (macOS):**
```env
GITHUB_TOKEN=ghp_xxxxxxxxxxxxxxxxxxxx
SPOTIFY_PATH=/Applications/Spotify.app
```

#### 🔑 Getting Your GitHub Token

1. Go to [GitHub Models](https://github.com/marketplace/models)
2. Sign in and navigate to Settings → Developer settings → Personal access tokens
3. Generate a new token with appropriate permissions
4. Copy and paste into your `.env` file

## ▶️ Usage

### Start JARVIS
```bash
python main.py
```

### 🎧 Interaction Modes

#### Wake-Word Mode (Default)
1. Say **"Jarvis"** or **"Hey Jarvis"**
2. Wait for the activation beep
3. Speak your command
4. JARVIS will respond

#### Push-to-Talk Mode
To enable, set in `main.py`:
```python
USE_WAKE_WORD = False
```

Then:
1. Press **SPACE** key
2. Speak your command
3. Release and wait for response

## 🗣 Voice Commands

| Command | Action |
|---------|--------|
| "Open Google" | Opens Google in browser |
| "Open YouTube" | Opens YouTube in browser |
| "Open Spotify" | Launches Spotify |
| "Play [song name]" | Plays song on YouTube |
| "Pause music" | Pauses current media |
| "Play music" / "Resume" | Resumes playback |
| "Next song" | Skips to next track |
| "Previous song" | Returns to previous track |
| "What is [topic]?" | AI-powered response |
| "Go to sleep" | Pauses wake-word detection |
| "Exit" / "Shutdown" | Closes JARVIS |

## 🎯 Design Philosophy

### Why Volume Ducking Instead of Auto-Pause?

**Problem:** System media keys are toggle-based, which can cause:
- ❌ Accidental playback when already paused
- ❌ User frustration
- ❌ Unreliable state management

**Solution:** Volume ducking
- ✅ Lowers volume during listening
- ✅ Restores volume after command
- ✅ Media state remains untouched
- ✅ Matches real-world assistant behavior

### AI Integration Approach

- GitHub Models provide **text-based** AI responses (free tier)
- Speech synthesis handled **locally** via pyttsx3
- Benefits:
  - ✅ Free to use
  - ✅ Stable and reliable
  - ✅ No API rate limits for TTS
  - ✅ Privacy-friendly

## 📂 Project Structure

```
jarvis-voice-assistant/
│
├── main.py              # Main assistant logic
├── .env                 # API keys (not committed to Git)
├── .gitignore           # Git ignore rules
├── requirements.txt     # Python dependencies
└── README.md            # This file
```

## 🚧 Known Limitations

- Wake-word detection requires internet (uses Google STT)
- Voice output quality depends on system TTS voices
- Spotify control uses system media keys (not official API)
- No conversation memory between sessions

## 🔮 Future Enhancements

- [ ] Offline wake-word detection (Vosk/Porcupine)
- [ ] Conversation history and memory
- [ ] GUI dashboard
- [ ] Smart home integration
- [ ] Multi-language support
- [ ] Custom AI voice models
- [ ] Spotify API integration

## 🐛 Troubleshooting

### Microphone not working
```bash
# Test microphone access
python -c "import speech_recognition as sr; print(sr.Microphone.list_microphone_names())"
```

### PyAudio installation issues (Windows)
```bash
pip install pipwin
pipwin install pyaudio
```

### GitHub API errors
- Verify your `GITHUB_TOKEN` in `.env`
- Check token permissions
- Ensure internet connection

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 👨‍💻 Author

**Yuvraj Gupta**
- Computer Science Student
- Passionate about Python, AI, and Automation

## 🙏 Acknowledgments

- Inspired by Marvel's JARVIS
- Built with Python and open-source libraries
- GitHub Models for free AI access

---

⭐ **If you find this project helpful, please consider giving it a star!**

📧 **Questions?** Feel free to open an issue or reach out!
