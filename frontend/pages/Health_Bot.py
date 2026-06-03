import streamlit as st
import streamlit.components.v1 as components
import json
import os

import sounddevice as sd
import scipy.io.wavfile as wav
import speech_recognition as sr

from utils.guards import require_auth, get_current_user
from utils.api import ask_chatbot
from components.ui import inject_custom_css, render_footer


# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="HealthAI Bot",
    layout="wide"
)

inject_custom_css()
require_auth()

user = get_current_user() or {}


# =========================
# LANGUAGE SETTINGS
# =========================
language_options = {
    "English": {
        "tts": "en-US",
        "speech": "en-US",
        "instruction": "Reply in simple English."
    },
    "हिंदी": {
        "tts": "hi-IN",
        "speech": "hi-IN",
        "instruction": "Reply in simple Hindi using Devanagari script."
    }
}

selected_language = st.sidebar.selectbox(
    "🌐 Language",
    list(language_options.keys())
)

tts_lang = language_options[selected_language]["tts"]
speech_lang = language_options[selected_language]["speech"]
language_instruction = language_options[selected_language]["instruction"]


# =========================
# VOICE OUTPUT
# =========================
def speak_text(text, lang_code):

    safe_text = json.dumps(text)

    components.html(
        f"""
        <script>
            window.speechSynthesis.cancel();

            const utterance = new SpeechSynthesisUtterance({safe_text});
            utterance.lang = "{lang_code}";
            utterance.rate = 0.95;
            utterance.pitch = 1;

            window.speechSynthesis.speak(utterance);
        </script>
        """,
        height=0
    )


def stop_voice():

    components.html(
        """
        <script>
            window.speechSynthesis.cancel();
        </script>
        """,
        height=0
    )


# =========================
# VOICE INPUT
# =========================
def recognize_speech(language_code):

    st.info("🎙️ Listening... Speak now")

    fs = 44100
    seconds = 5
    temp_filename = "temp_voice.wav"

    try:
        recording = sd.rec(
            int(seconds * fs),
            samplerate=fs,
            channels=1,
            dtype="int16"
        )

        sd.wait()

        wav.write(
            temp_filename,
            fs,
            recording
        )

        recognizer = sr.Recognizer()

        with sr.AudioFile(temp_filename) as source:
            audio_data = recognizer.record(source)

            text = recognizer.recognize_google(
                audio_data,
                language=language_code
            )

        if os.path.exists(temp_filename):
            os.remove(temp_filename)

        return text

    except Exception as e:

        if os.path.exists(temp_filename):
            os.remove(temp_filename)

        st.error(f"Voice input error: {e}")

        return None


# =========================
# SESSION STATE
# =========================
if "messages" not in st.session_state:
    st.session_state.messages = []

if "last_response" not in st.session_state:
    st.session_state.last_response = ""

if "voice_prompt" not in st.session_state:
    st.session_state.voice_prompt = ""


# =========================
# SIDEBAR CONTROLS
# =========================
with st.sidebar:

    st.markdown("### 🛠️ Bot Controls")

    if st.button(
        "🔇 Stop Voice",
        use_container_width=True
    ):
        stop_voice()
        st.success("Voice stopped")

    if st.button(
        "🗑️ Clear Chat",
        use_container_width=True
    ):
        st.session_state.messages = []
        st.session_state.last_response = ""
        st.session_state.voice_prompt = ""
        st.rerun()

    st.caption(
        f"Current Language: {selected_language}"
    )


# =========================
# HEADER
# =========================
st.title("💬 HealthAI Clinical Assistant")

st.caption(
    "Ask health-related questions using text or voice. The assistant replies with text and speech."
)


# =========================
# INITIAL MESSAGE
# =========================
if not st.session_state.messages:

    welcome_msg = (
        f"Hello {user.get('username', 'User')}, "
        "how can I help you with your health query today?"
    )

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": welcome_msg
        }
    )


# =========================
# DISPLAY CHAT HISTORY
# =========================
for msg in st.session_state.messages:

    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])


# =========================
# VOICE INPUT BUTTON
# =========================
st.markdown("### 🎤 Voice Input")

if st.button(
    "🎙️ Ask with Voice",
    use_container_width=True
):

    detected_text = recognize_speech(
        speech_lang
    )

    if detected_text:

        st.success(
            f"You said: {detected_text}"
        )

        st.session_state.voice_prompt = detected_text


# =========================
# TEXT INPUT
# =========================
typed_prompt = st.chat_input(
    "Type your health question..."
)

voice_prompt = st.session_state.get(
    "voice_prompt",
    ""
)

prompt = voice_prompt or typed_prompt


# =========================
# PROCESS PROMPT
# =========================
if prompt:

    st.session_state.voice_prompt = ""

    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt
        }
    )

    with st.chat_message("user"):
        st.markdown(prompt)

    final_prompt = f"""
    {language_instruction}

    User question:
    {prompt}

    Give safe healthcare guidance.
    Keep the answer simple and useful.
    Include a short disclaimer that this is AI-generated advice
    and not a replacement for a doctor.
    """

    with st.chat_message("assistant"):

        with st.spinner("Generating response..."):

            response = ask_chatbot(
                st.session_state.token,
                final_prompt
            )

            if response.status_code == 200:

                bot_reply = response.json().get(
                    "response",
                    "No response received."
                )

            else:

                bot_reply = (
                    f"Failed to get chatbot response. "
                    f"Status: {response.status_code} - {response.text}"
                )

        st.markdown(bot_reply)

        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": bot_reply
            }
        )

        st.session_state.last_response = bot_reply

        speak_text(
            bot_reply,
            tts_lang
        )


# =========================
# REPLAY / STOP
# =========================
if st.session_state.last_response:

    c1, c2 = st.columns(2)

    with c1:

        if st.button(
            "🔊 Replay Last Response",
            use_container_width=True
        ):
            speak_text(
                st.session_state.last_response,
                tts_lang
            )

    with c2:

        if st.button(
            "🔇 Stop Speaking",
            use_container_width=True
        ):
            stop_voice()


