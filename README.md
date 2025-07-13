# CookSense Assistant

A smart assistant designed to help users with cooking queries via both voice and text. Built using **Gradio**, **OpenAI GPT**, and speech libraries, CookSense Assistant offers hands-free transcription, chat replies, and voice output — perfect for kitchen environments.

---

## Features

- ChatGPT-style conversational interface
- Voice input using microphone (speech-to-text via `SpeechRecognition`)
- Spoken replies with `gTTS` (Google Text-to-Speech)
- Custom assistant personality via system prompt
- Friendly greeting message on startup
- OpenAI API key secured with `.env` file

---

## Getting Started
1. Clone the Repository
[In terminal]
git clone https://github.com/AzureSnake/HCI%20CookSense%20Assistant.git
cd cooksense-assistant

2. Install Required Packages
Make sure you're using Python 3.10+, then install all dependencies:
[In terminal]
pip install -r requirements.txt

3. Create a .env File
Create a .env file in the root directory and add your OpenAI API key:
OPENAI_API_KEY=[your_openai_api_key_here]

4. Run the App
[In terminal]
python app.py

Dependencies
All listed in requirements.txt:

openai

gradio

gtts

speechrecognition

python-dotenv