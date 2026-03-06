# 🎤 Speech-to-Text Web Assistant

A Python-based voice assistant that records speech from your microphone, converts it into text using **OpenAI Whisper**, and automatically searches the web to provide an answer.

This tool listens for your voice, detects when you start and stop speaking, transcribes the speech, and fetches relevant information from the internet.

The assistant runs entirely on **CPU**, so it works even on systems without a GPU.

---

# 🚀 Features

* 🎤 Automatic microphone recording
* 🧠 Speech recognition using Whisper
* 🔇 Smart silence detection (auto stop recording)
* 🌐 Web search integration
* 📄 Automatic webpage text extraction
* ⚡ Runs on CPU (no GPU required)

---

# 📂 Project Structure

```
project-folder
│
├── speechtotext.py
└── README.md
```

`speechtotext.py` contains the complete implementation of the speech recognition and web search assistant.

---

# 🧰 Requirements

You need **Python 3.9 or newer**.

Required Python libraries:

* sounddevice
* scipy
* transformers
* numpy
* duckduckgo-search
* requests
* beautifulsoup4
* torch

---

# 📦 Installation

## 1. Clone the repository

```
git clone https://github.com/AsjadAbbas995/Speech-To-Text-Chatbot.git
cd YOUR_REPOSITORY
```

---

## 2. (Optional but Recommended) Create a Virtual Environment

### Windows

```
python -m venv venv
venv\Scripts\activate
```

### Linux / Mac

```
python3 -m venv venv
source venv/bin/activate
```

---

## 3. Install Dependencies

```
pip install sounddevice scipy transformers numpy duckduckgo-search requests beautifulsoup4 torch
```

---

# ▶️ Running the Program

Run the script:

```
python speechtotext.py
```

You will see:

```
🎤 Speech-to-Text Web Assistant (CPU)
Press Enter to start listening
```

Press **Enter** and begin speaking.

The program will:

1. Calibrate microphone noise
2. Detect when you start speaking
3. Record your voice
4. Stop when silence is detected
5. Convert speech to text
6. Search the web
7. Display the answer

---

# ⚙️ How It Works

### 1. Audio Recording

Audio is captured using the **sounddevice** library and processed in small chunks.

### 2. Speech Detection

The program calculates the RMS volume of the audio to determine whether speech is present.

### 3. Speech Recognition

Speech is transcribed using the **Whisper Base model** through the HuggingFace Transformers pipeline.

### 4. Web Search

The recognized text is used as a search query. The assistant retrieves results using DuckDuckGo and extracts information from the top webpage.

---

# 🖥 System Requirements

Minimum recommended:

* 8 GB RAM
* Microphone
* Internet connection
* Python 3.9+

Note: The first run will download the Whisper model, which may take a few minutes.

---

# ⚠️ Known Limitations

* Performance may drop in noisy environments
* Some websites block scraping
* Responses are extracted text, not AI-generated summaries

---

# 🔧 Future Improvements

Possible upgrades:

* Add GPT-based answers
* Implement text-to-speech responses
* Add a graphical user interface
* Enable continuous conversation mode
* Improve speech detection

---

# 📜 License

This project is intended for educational and personal use.
