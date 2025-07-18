# === chatbot_logic.py ===
import io
import json
import boto3
import base64
import datetime
import tempfile
from gtts import gTTS
from pydub import AudioSegment
from langchain.chains import ConversationChain
from langchain.memory import ConversationSummaryBufferMemory
from langchain_aws import ChatBedrock
import speech_recognition as sr

# ✅ AWS region setup
AWS_REGION = 'us-east-1'

# ✅ Initialize AWS Bedrock client
client_bedrock = boto3.client('bedrock-runtime', region_name=AWS_REGION)

# ✅ Initialize the Claude model from Bedrock
def get_llm_model():
    return ChatBedrock(
        credentials_profile_name='default',
        model_id='anthropic.claude-3-sonnet-20240229-v1:0',
        model_kwargs={
            "max_tokens": 300,
            "temperature": 0.1,
            "top_p": 0.9,
            "stop_sequences": ["\n\nHuman:"]
        }
    )

# ✅ Generate conversational response
def generate_response(input_text, llm, memory):
    chain = ConversationChain(llm=llm, memory=memory, verbose=False)
    result = chain.invoke(input=input_text)
    return result['response']

# ✅ Convert mic audio bytes to text using SpeechRecognition
def speech_bytes_to_text(audio_bytes):
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as wav_file:
            audio = AudioSegment.from_file(io.BytesIO(audio_bytes))
            audio.export(wav_file.name, format="wav")

            recognizer = sr.Recognizer()
            with sr.AudioFile(wav_file.name) as source:
                audio_data = recognizer.record(source)
                return recognizer.recognize_google(audio_data)
    except Exception as e:
        return f"❌ Error in transcription: {e}"

# ✅ Correct grammar using Claude
def correct_grammar(text):
    import json
    import boto3

    client_bedrock = boto3.client('bedrock-runtime', region_name='us-east-1')

    system_prompt = (
        "You are an expert English grammar assistant. "
        "You will receive a grammatically incorrect sentence, "
        "and you must return ONLY the corrected version. "
        "Do not include any explanations or additional text."
    )

    prompt = (
        f"\n\nHuman: Correct this sentence and return only the corrected version:\n{text}\n\nAssistant:"
    )

    response = client_bedrock.invoke_model(
        modelId='anthropic.claude-instant-v1',
        body=json.dumps({
            "prompt": system_prompt + prompt,
            "max_tokens_to_sample": 100,
            "temperature": 0.5
        }),
        contentType="application/json",
        accept="application/json"
    )

    result = json.loads(response['body'].read())
    return result['completion'].strip()

# ✅ Suggest practice topics using Claude
def suggest_topic():
    system_prompt = (
        "You are a conversation coach. Suggest one engaging and simple topic "
        "for someone to practice speaking English. Just return the topic as a sentence or question."
    )
    prompt = "\n\nHuman: Suggest one topic for English speaking practice.\nAssistant:"

    response = client_bedrock.invoke_model(
        modelId='anthropic.claude-instant-v1',
        body=json.dumps({
            "prompt": system_prompt + prompt,
            "max_tokens_to_sample": 50,
            "temperature": 0.7
        }),
        contentType="application/json",
        accept="application/json"
    )

    result = json.loads(response['body'].read())
    return result['completion'].strip()

# ✅ Text-to-Speech using gTTS
def text_to_speech(text, filename="response.mp3"):
    try:
        tts = gTTS(text=text, lang='en')
        tts.save(filename)
        return filename
    except Exception as e:
        print(f"TTS error: {e}")
        return None