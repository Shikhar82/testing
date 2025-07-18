import streamlit as st
import chatbot_logic as logic
from langchain.memory import ConversationSummaryBufferMemory
from streamlit_mic_recorder import mic_recorder
from streamlit_lottie import st_lottie
import json
import base64

# --- Meta Tags ---
st.markdown("""
    <meta property="og:title" content="AI Spoken English Chatbot | Shikhar Verma">
    <meta property="og:description" content="Practice spoken English with AI feedback and voice response.">
    <meta property="og:image" content="https://www.chatbotshikhar.com/courselogo.png">
    <meta property="og:url" content="https://www.chatbotshikhar.com">
    <meta name="twitter:card" content="summary_large_image">
""", unsafe_allow_html=True)

# --- Page Config ---
st.set_page_config(
    page_title="Spoken English Chatbot",
    page_icon="https://www.chatbotshikhar.com/courselogo.png",
    layout="centered"
)

# --- Load Animation ---
def load_lottie_file(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)

lottie_robot = load_lottie_file("robot.json")

# --- Header ---
with st.container():
    col1, col2 = st.columns([1.5, 6])
    with col1:
        st.markdown("<div style='margin-top: -50px; margin-bottom: -20px;'>", unsafe_allow_html=True)
        st_lottie(lottie_robot, height=150, key="robot")
        st.markdown("</div>", unsafe_allow_html=True)
    with col2:
        st.markdown("""
            <h1 style='margin-bottom: 4px; font-size: 2.1rem;'>🎙️ AI Spoken English Chatbot</h1>
            <p style='margin-top: 0px; font-size: 1.05rem;'>Improve your spoken English by talking to the bot and getting grammar corrections!</p>
        """, unsafe_allow_html=True)

# --- Session Setup ---
if 'llm' not in st.session_state:
    st.session_state.llm = logic.get_llm_model()

if 'memory' not in st.session_state:
    st.session_state.memory = ConversationSummaryBufferMemory(llm=st.session_state.llm, max_token_limit=300)

if 'messages' not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "👋 Hello! What topics do you enjoy talking about in English?"}
    ]

# --- Display chat history ---
for i in range(0, len(st.session_state.messages), 2):
    user_msg = st.session_state.messages[i]
    ai_msg = st.session_state.messages[i+1] if i+1 < len(st.session_state.messages) else None

    if user_msg["role"] == "user":
        st.chat_message("user").markdown(user_msg["content"])
        if ai_msg and ai_msg["role"] == "assistant":
            st.chat_message("assistant").markdown(ai_msg["content"])
    else:
        st.chat_message("assistant").markdown(user_msg["content"])

# --- Mic Input Section ---
st.subheader("🎙️ Speak into the Mic to Practice")

audio_bytes = mic_recorder(start_prompt="Click to Speak", stop_prompt="Stop", just_once=True, key="mic")

if audio_bytes and 'bytes' in audio_bytes:
    st.audio(audio_bytes['bytes'], format='audio/wav')
    transcribed = logic.speech_bytes_to_text(audio_bytes['bytes'])

    if transcribed:
        st.chat_message("user").markdown(transcribed)
        st.session_state.messages.append({"role": "user", "content": transcribed})

        corrected = logic.correct_grammar(transcribed)
        st.chat_message("assistant").markdown(f"✍️ **Corrected**: {corrected}")

        with st.spinner("🤖 Thinking..."):
            response = logic.generate_response(corrected, st.session_state.llm, st.session_state.memory)

        st.session_state.messages.append({"role": "assistant", "content": response})

        st.markdown("""
        <div style="text-align:center; margin-bottom: 10px;">
            <img src="https://www.chatbotshikhar.com/assets/ai_talking.gif" width="150">
        </div>
        """, unsafe_allow_html=True)

        st.chat_message("assistant").markdown(response)

        audio_path = logic.text_to_speech(response)
        if audio_path:
            with open(audio_path, "rb") as audio_file:
                audio_data = audio_file.read()
                encoded_audio = base64.b64encode(audio_data).decode()

                st.markdown(f"""
                    <audio id="ai_audio" autoplay controls style="width: 100%; margin-top: 10px;">
                        <source src="data:audio/mp3;base64,{encoded_audio}" type="audio/mp3">
                        Your browser does not support the audio element.
                    </audio>
                """, unsafe_allow_html=True)

# --- Suggest Topic ---
if st.button("💡 Suggest a Speaking Topic"):
    topic = logic.suggest_topic()
    st.chat_message("assistant").markdown(f"🗣️ Try speaking on: **{topic}**")

# --- Text Input Section ---
user_input = st.chat_input("💬 Type your message to the AI...")

if user_input:
    st.chat_message("user").markdown(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})

    corrected = logic.correct_grammar(user_input)
    st.chat_message("assistant").markdown(f"✍️ **Corrected**: {corrected}")

    with st.spinner("🤖 Thinking..."):
        response = logic.generate_response(corrected, st.session_state.llm, st.session_state.memory)

    st.session_state.messages.append({"role": "assistant", "content": response})

    st.markdown("""
    <div style="text-align:center; margin-bottom: 10px;">
        <img src="https://www.chatbotshikhar.com/assets/ai_talking.gif" width="150">
    </div>
    """, unsafe_allow_html=True)

    st.chat_message("assistant").markdown(response)

    audio_path = logic.text_to_speech(response)
    if audio_path:
        with open(audio_path, "rb") as audio_file:
            audio_data = audio_file.read()
            encoded_audio = base64.b64encode(audio_data).decode()

            st.markdown(f"""
                <audio id="ai_audio" autoplay controls style="width: 100%; margin-top: 10px;">
                    <source src="data:audio/mp3;base64,{encoded_audio}" type="audio/mp3">
                    Your browser does not support the audio element.
                </audio>
            """, unsafe_allow_html=True)

# --- Footer ---
st.markdown("""
<hr style="margin-top:30px;">
<div style='text-align: center; color: gray'>
    Created by Shikhar Verma | 💬 AI Spoken English Chatbot | Powered by AWS Bedrock
</div>
""", unsafe_allow_html=True)

