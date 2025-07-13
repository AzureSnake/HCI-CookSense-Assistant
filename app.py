import os
import gradio as gr
from openai import OpenAI
from gtts import gTTS
from dotenv import load_dotenv
import speech_recognition as sr

# Load .env and initialize OpenAI
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# System prompt and greeting
SYSTEM_PROMPT = {"role": "system", "content": "You are CookSense Assistant, a friendly and knowledgeable "
"virtual cooking guide designed to help users learn cooking techniques through AR-based step-by-step guidance. "
"You offer support in understanding tasks, clarifying instructions, and helping users navigate recipes, "
"basic tasks, and full meals. Always respond in clear, encouraging, and simple language suitable for "
"beginners. Provide helpful tips where necessary, but avoid performing tasks for the user. You must stay "
"within the scope of cooking help. Do not provide unrelated advice (e.g., health, medical, or "
"financial advice). When a user asks for help, check their current step, context "
"(basic task, single recipe, full meal), and respond based on that. If a user gets stuck, offer "
"suggestions to retry, rewind, or view a short tip video. If confusion continues, offer to "
"escalate to a visual overlay or basic task breakdown. Do not guess. If unsure, say: "
"Let’s look at this together! and guide them back to a safe, learnable step."}

GREETING = "Ready to level up your cooking skills? Choose a task, recipe, or full meal — I’ll guide you step by step!"

# Global chat history
chat_history = [SYSTEM_PROMPT]

# TTS
def text_to_speech(text):
    tts = gTTS(text)
    filename = "tts_output.mp3"
    tts.save(filename)
    return filename

# STT using SpeechRecognition
def transcribe(audio_file):
    recognizer = sr.Recognizer()
    if not audio_file:
        return "[Error] No audio file received."
    try:
        with sr.AudioFile(audio_file) as source:
            audio = recognizer.record(source)
            return recognizer.recognize_google(audio)
    except sr.UnknownValueError:
        return "[Error] Could not understand audio."
    except sr.RequestError as e:
        return f"[Error] STT request failed: {e}"
    except Exception as e:
        return f"[Error] {str(e)}"

# Greeting on page load
def init_chat():
    chat_history.append({"role": "assistant", "content": GREETING})
    return chat_history, "", text_to_speech(GREETING)

# Chat function
def chat_fn(user_msg, _, history):
    if not user_msg.strip():
        return history, "", None

    chat_history.append({"role": "user", "content": user_msg})
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=chat_history
    )
    reply = response.choices[0].message.content.strip()
    chat_history.append({"role": "assistant", "content": reply})

    return chat_history, "", text_to_speech(reply)

# Gradio UI
with gr.Blocks() as demo:
    gr.Markdown("## 🤖 CookSense Chatbot Assistant")

    chatbot = gr.Chatbot(type="messages", label="Chat History")
    user_input = gr.Textbox(show_label=False, placeholder="Type a message and press Enter")
    send_btn = gr.Button("Send")

    with gr.Row():
        audio_input = gr.Audio(sources=["microphone", "upload"], type="filepath", label="🎙️ Speak or Upload Audio")
        transcribe_btn = gr.Button("Transcribe")

    tts_out = gr.Audio(label="🔊 Bot Voice")

    # Hooks
    demo.load(fn=init_chat, outputs=[chatbot, user_input, tts_out])
    send_btn.click(chat_fn, [user_input, chatbot, chatbot], [chatbot, user_input, tts_out])
    user_input.submit(chat_fn, [user_input, chatbot, chatbot], [chatbot, user_input, tts_out])
    def transcribe_to_input(audio_file):
        text = transcribe(audio_file)
        return gr.update(value=text)  # sets it in user_input textbox only

    transcribe_btn.click(
        transcribe_to_input,
        inputs=audio_input,
        outputs=user_input
    )

demo.launch()
